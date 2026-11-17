const BATCH_NUM=150;
export default {
inject:['service', 'tags'],
data() {return {
    devices:[],
    products:[],
    total:0,
    product:'0',//当前选中的产品
    options:[],
    page:{cur:1, max:0},
    percent:{val:0, each:0},
    devInfo:{dlg:false,codes:[],createAt:''},
    errList:''
}},
created() {
    this.service.getProducts(true).then(products => {
        if(!products || products.length==0) {
            this.$refs.errDlg.show(this.tags.noProducts);
            return;
        }
        this.products=products;
        var opts=[];
        for(var i in products) {
            var p=products[i];
            opts.push({label:p.name+'('+p.prefix+')', value:i});
        }
        this.options=opts;
        this.devInfo.createAt=new Date().toLocaleDateString();
        this.query_devices(1);
    });
},
methods:{
query_devices(pg) {
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var prt=this.products[parseInt(this.product)].id;
    var url = "/api/device/list?offset="+offset+"&num="+this.service.N_PAGE+"&product="+prt;
    request({method:"GET",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK || resp.data.total==0) {
            this.devices=[];
            this.page.max=0;
            this.page.cur=1;
            this.total=0;
            return;
        }
        this.fmt_lines(resp.data);
        this.total=resp.data.total;
        this.page.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
fmt_lines(data) {
    var dt=new Date();
    var devices=[];
    var cols=data.cols;
    var dev;
    for(var row of data.devices) {
        dev={};
        for(var i in cols) {
            dev[cols[i]]=row[i];
        }
        dt.setTime(dev.createAt*60000);
        dev.createAt=date2str(dt);
        if(dev.sellAt>0) {
            dt.setTime(dev.sellAt*60000);
            dev.sellAt=date2str(dt);
        } else {
            dev.sellAt=this.tags.notSell;
        }
        devices.push(dev);
    }
    this.devices=devices;
},
addDevice(){
    var prt=this.products[parseInt(this.product)];
    var createAt=new Date(this.devInfo.createAt).getTime()/60000;//utc分钟
    var codes=this.devInfo.codes.split(/[(\r\n)\r\n\s\t,;]+/);
    this.invalid=[];
    this.percent.val=0;
    if(codes.length<BATCH_NUM) {
        this.percent.each=0;//不显示
    } else {
        var n=Math.ceil(codes.length/BATCH_NUM);
        this.percent.each=1.0/n;
    }
    this.add_batch(codes, prt, createAt, 0);
},
add_batch(codes, prt, createAt, start) {
    var dta={product:prt.id,createAt:createAt,codes:[]};
    var c;
    var invalid=[];
    for(var n=0,i=start,l=codes.length; i<l&&n<BATCH_NUM; i++,n++) {
        c=codes[i];
        if(c.length>prt.codeLen) {
            if(c.startsWith(prt.prefix) && c.length==prt.totalLen) { 
                dta.codes.push(c.substring(prt.prefix.length));
            } else {
                invalid.push(c);
            }
        } else if(c.length==prt.codeLen) {
            dta.codes.push(c);
        } else if(c.length>0){
            invalid.push(c);
        }
    }
    
    if(invalid.length > 0) {
        var s=[this.tags.invalidCode, "\n"];
        var n=0;
        for(var c of invalid) {
            if(n>0)s.push(',');
            s.push(c);
            n++;
        }
        this.errList=s.join('');
        return;
    }
    
    request({method:"POST",url:"/api/device/add",data:dta}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK) {
            this.$refs.errDlg.showErr(resp.code, resp.info);
            this.percent.val=0;
            return;
        }

        this.percent.val+=this.percent.each;
        if(start+BATCH_NUM < codes.length) {
            this.add_batch(codes, prt, createAt, start+BATCH_NUM);
            return;
        }
        this.query_devices(1);
        this.percent.val=0;
        this.devInfo.dlg=false;
    });    
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat round icon="arrow_back" dense @click="service.go_back"></q-btn>
    <q-toolbar-title>{{tags.deviceMng}}</q-toolbar-title>
   </q-toolbar>
  </q-header>
  <q-footer class="bg-white" v-if="service.role!='customer'">
   <q-list><q-item>
    <q-item-section side>{{tags.device.product}}</q-item-section>
    <q-item-section>
      <q-select v-model="product" emit-value map-options :options="options" dense
      @update:model-value="query_devices(1)"></q-select>
    </q-item-section>
    <q-item-section side>
     <q-chip><q-avatar icon="bookmark" color="red" text-color="white"></q-avatar>{{total}}</q-chip>
    </q-item-section>
    <q-item-section side>
      <q-btn round color="primary" icon="playlist_add" @click="devInfo.dlg=true" v-if="service.role!='customer'"></q-btn>
    </q-item-section>
   </q-item></q-list>
  </q-footer>
<q-page-container>
    <q-page class="q-pa-md">
<div class="q-pa-sm flex flex-center" v-if="page.max>1">
 <q-pagination v-model="page.cur" color="primary" :max="page.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query_devices"></q-pagination>
</div>
<q-markup-table flat>
<thead><tr>
 <th>{{tags.device.code}}</th>
 <th>{{tags.device.createAt}}</th>
 <th>{{tags.device.sellAt}}</th>
</tr></thead>
<tbody>
<tr v-for="d in devices">
 <td>{{d.code}}</td>
 <td>{{d.createAt}}</td>
 <td>{{d.sellAt}}</td>
</tr>
</tbody>
</q-markup-table>
    </q-page>
  </q-page-container>
</q-layout>

<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" :close="tags.close" ref="errDlg"></component-alert-dialog>

<!-- 增加设备 -->
<q-dialog v-model="devInfo.dlg" no-backdrop-dismiss>
  <q-card style="min-width:75vw">
    <q-linear-progress :value="percent.val" color="pink" v-show="percent.val>0"></q-linear-progress>
    <q-card-section>
     <div class="text-h6">{{tags.addDevice}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
    <q-list>
      <q-item><q-item-section>
       <component-date-input :close="tags.ok" :label="tags.device.createAt" v-model="devInfo.createAt"></component-date-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-input v-model="devInfo.codes" :label="tags.device.code"
        dense maxlength=100000 type="textarea" rows="12"></q-input>
      </q-item-section></q-item>
    </q-list>
    </q-card-section>
    <q-card-section v-show="errList!=''">
     <div class="text-red" style="word-wrap:break-word;white-space:pre-wrap;">{{errList}}</div>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.ok" color="primary" @click.stop="addDevice"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>
`
}