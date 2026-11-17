export default {
inject:['service', 'tags'],
data() {return {
    id:this.$route.query.id,
    dtl:{},
    ctrl:{editable:false,editing:false,edt:{}/*编辑内容*/},

    skuList:[],
    purList:[],
    skuCtrl:{dlg:false, dta:{},sku:{}/*用在SkuSelector中输入sku*/}
}},
created(){
    this.query();
    this.grn_list();
},
methods:{
query() {
    var url="/grn/get?id="+this.id+"&factory="+this.dtl.factory;
    request({method:"GET", url:url}, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            return;
        }
        var p=resp.data;
        this.ctrl.editable=p.state=='WAIT'||p.state=='CHK';
        //outDate,inDate,type,state,tranNo,cmt,execAcc,prjName,applicant
        var dt=new Date();
        dt.setTime(p.inDate*60000);
        p.inDate=date2str(dt);
        dt.setTime(p.outDate*60000);
        p.outDate_s=date2str(dt);
        p.type=this.tags.grnType[p.type];
        p.state=this.tags.grnState[p.state];
        this.dtl=p;
        this.pur_list();
    })
},
show_edit() {
    this.ctrl.editing=true;
    copyObjTo(this.dtl, this.ctrl.edt);
},
update() {
    var dta=copyObj(this.ctrl.edt, ['tranNo','cmt']);
    dta.id=this.id;
    dta.factory=this.dtl.factory;
    dta.outDate=parseInt(Date.parse(this.ctrl.edt.outDate_s)/60000);
    request({method:"PUT", url:"/grn/update", data:dta}, this.service.name).then(resp=>{
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.ctrl.editing=false;
        copyObjTo(this.ctrl.edt, this.dtl, ['tranNo','outDate_s','cmt']);
    });
},
remove() {
    this.$refs.cfmDlg.show(this.tags.cfmRmv, ()=>{
        var opts={method:"DELETE",url:"/grn/remove?purId="+this.id+"&factory="+this.dtl.factory};
        request(opts, this.service.name).then(resp => {
            if(resp.code!=RetCode.OK) {
                this.$refs.alertDlg.showErr(resp.code, resp.info);
                return;
            }
            this.service.back();
        })
    });
},
grn_list() {
    var url="/grn/grnlist?grnId="+this.id;
    request({method:"GET", url:url}, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            return;
        }
        this.skuList=resp.data.list;
    })
},
pur_list() { //采购单申请的sku列表
    var url="/purchase/skulist?id="+this.dtl.purId;
    request({method:"GET", url:url}, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            return;
        }
        var skus=resp.data.skus;//id->[speci,noHead]
        this.purList=resp.data.list.map(p=>{
            var sku=skus[p.sku];
            if(sku) {
                p.speci=sku[0];
                p.noHead=sku[1];
            } else {
                p.speci='';
                p.noHead='';
            }
            return p;
        });
    })
},
show_ship() {
    this.skuCtrl.dta={sku:0,num:'',cmt:''};
    this.skuCtrl.dlg=true;
},
ship_in() {
    var sku=this.skuCtrl.sku;
    var d=this.skuCtrl.dta;
    if(!sku.id||!d.num)return;
    var dta={sku:sku.id,num:d.num,cmt:d.cmt, grnId:this.id,
        purId:this.dtl.purId,factory:this.dtl.factory};

    var opts={method:"POST", url:"/grn/shipIn", data:dta};
    request(opts, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.grn_list();
        this.skuCtrl.dlg=false;
    });
},
remove_sku(i) {
    var url="/grn/removeSku?purId="+this.id
        +"&factory="+this.dtl.factory+"&no="+this.skuList[i].no;
    request({method:"DELETE", url:url}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.skuList.splice(i,1);
    });
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat icon="arrow_back" dense @click="service.back()"></q-btn>
     <q-toolbar-title>{{tags.grn.title}}</q-toolbar-title>
     <q-btn flat icon="clear" @click="remove" v-if="ctrl.editable&&!ctrl.editing" dense></q-btn>
     <q-btn flat icon="edit" @click="show_edit" v-if="ctrl.editable&&!ctrl.editing" dense></q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-sm">
<q-list dense>
  <q-item>
    <q-item-section>{{tags.prjName}}</q-item-section>
    <q-item-section side>{{dtl.prjName}}</q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.applicant}}</q-item-section>
    <q-item-section side>{{dtl.applicant}}</q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.type}}</q-item-section>
    <q-item-section side>{{dtl.type}}</q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.state}}</q-item-section>
    <q-item-section side>{{dtl.state}}</q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.storage.execAcc}}</q-item-section>
    <q-item-section side>{{dtl.execAcc}}</q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.storage.inDate}}</q-item-section>
    <q-item-section side>{{dtl.inDate}}</q-item-section>
  </q-item>
</q-list>
<q-list dense v-if="!ctrl.editing">
  <q-item>
    <q-item-section>{{tags.storage.outDate}}</q-item-section>
    <q-item-section side>{{dtl.outDate_s}}</q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.storage.tranNo}}</q-item-section>
    <q-item-section side>{{dtl.tranNo}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.cmt}}</q-item-section>
   <q-item-section side>{{dtl.cmt}}</q-item-section>
  </q-item>
</q-list>
<div v-else>
  <date-input v-model="ctrl.edt.outDate_s" :label="tags.storage.outDate"
  :format="tags.dateFmt"></date-input>
  <q-input v-model="ctrl.edt.tranNo" :label="tags.storage.tranNo"></q-input>
  <q-input v-model="ctrl.edt.cmt" :label="tags.cmt"></q-input>
  <div class="row justify-end q-py-md">
    <div class="col-2">
      <q-btn flat :label="tags.cancel" @click="ctrl.editing=false" color="primary"></q-btn>
    </div>
    <div class="col-2">
      <q-btn :label="tags.ok" @click="update" color="primary"></q-btn>
    </div>
  </div>
</div>

<q-banner inline-actions dense class="q-mb-sm text-dark bg-blue-grey-1">
  {{tags.purchase.skuList}}
</q-banner>
<q-list dense separator>
  <q-item>
   <q-item-section><q-item-label caption>{{tags.sku.title}}</q-item-label></q-item-section>
   <q-item-section><q-item-label caption>{{tags.num}}</q-item-label></q-item-section>
   <q-item-section><q-item-label caption>{{tags.sku.price}}</q-item-label></q-item-section>
   <q-item-section side><q-item-label caption>{{tags.sku.noHead}}</q-item-label></q-item-section>
  </q-item>
  <q-item v-for="(e,i) in purList">
    <q-item-section>{{e.skuName}}</q-item-section>
    <q-item-section>{{e.num}}</q-item-section>
    <q-item-section>{{e.price}}</q-item-section>
    <q-item-section side>{{e.noHead}}</q-item-section>
  </q-item>
</q-list>

<q-banner inline-actions dense class="q-mb-sm text-dark bg-blue-grey-1">
  {{tags.grn.skuList}}
  <template v-slot:action v-if="ctrl.editable">
    <q-icon name="add_circle" @click="show_ship" color="primary"></q-icon>
  </template>
</q-banner>
<q-list dense separator>
  <q-item v-for="(e,i) in skuList">
   <q-item-section>
    <q-item-label>{{e.no}}</q-item-label>
    <q-item-label caption>{{e.skuName}}</q-item-label>
   </q-item-section>
   <q-item-section>{{e.num}}</q-item-section>
   <q-item-section side v-if="ctrl.editable">
     <q-btn icon="clear" @click="remove_sku(i)" flat dense color="red"></q-btn>
   </q-item-section>
  </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="skuCtrl.dlg">
 <q-card style="min-width:70vw">
  <q-card-section>
   <div class="text-h6">{{tags.grn.skuList}}</div>
   <q-separator></q-separator>
  </q-card-section>
  <q-card-section class="q-pt-none">
    <sku-select v-model="skuCtrl.sku" :label="tags.sku.title"></sku-select>
    <q-input v-model.number="skuCtrl.dta.num" :label="tags.num" type="number"></q-input>
    <q-input v-model="skuCtrl.dta.cmt" :label="tags.cmt"></q-input>
  </q-card-section>
  <q-card-actions align="right">
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    <q-btn :label="tags.ok" color="primary" @click="ship_in"></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="alertDlg"></alert-dialog>
<confirm-dialog :title="tags.attention" :ok="tags.ok"
 :close="tags.cancel" ref="cfmDlg"></confirm-dialog>
`
}