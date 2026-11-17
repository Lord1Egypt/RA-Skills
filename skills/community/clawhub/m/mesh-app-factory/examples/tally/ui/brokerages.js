const MINUTE_MS=60000;
const YEAR_MS=31622400000;
import {decodeExt} from '/assets/v3/settings/config.js';
import ServiceDlg from "./servicedlg.js"
import OrderDlg from "./orderdlg.js"

export default {
inject:['service', 'tags'],
components:{
    "service-dlg":ServiceDlg,
    "order-dlg":OrderDlg
},
data() {return {
    role:'',
    list:[], //佣金列表
    range:{from:'',to:''},
    ctrl:{cur:1,max:0,owner:'',dlg:false},
    cmt:{cur:1,max:0,owner:'',dlg:false,list:[]},
    dtl:{cur:1,max:0,owner:'',dlg:false,list:[]},
    user:{account:'',dlg:false,dtl:{},segs:[],tmpl:{}}
}},
created(){
    var dt=new Date();
    var cur=parseInt(dt.getTime()/MINUTE_MS)+1440;
    dt.setTime(cur*MINUTE_MS);
    this.range.to=date2str(dt);
    dt.setTime((cur-1440*6)*MINUTE_MS);
    this.range.from=date2str(dt);
    
    this.service.getRole().then(role=>{
        this.role=role;
        this.query(1);
    })
},
methods:{
query(pg) {
    var to=parseInt(new Date(this.range.to).getTime()/MINUTE_MS)+1440;//包括最后一天
    var from=parseInt(new Date(this.range.from).getTime()/MINUTE_MS);
    var offset=(parseInt(pg)-1)*this.service.NUM_PER_PAGE;
    var url="/report/brokerages?offset="+offset
        +"&num="+this.service.NUM_PER_PAGE
        +"&from="+from+"&to="+to;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.list=[];
            this.ctrl.max=0;
        } else {
            var cols=resp.data.cols;
            this.list=resp.data.list.map(l=>{
                var r={};
                for(var i in cols) {
                    r[cols[i]]=l[i];
                }
                return r;
            })
            this.ctrl.max=Math.ceil(resp.data.total/this.service.NUM_PER_PAGE);
        }
    })
},
dateChanged() {
    this.ctrl.cur=1;
    this.query(1);
},
show_detail(owner) {
    this.dtl.owner=owner;
    this.dtl.dlg=true;
    this.query_dtl(1);
},
query_dtl(pg) {
    var to=parseInt(new Date(this.range.to).getTime()/MINUTE_MS)+1440; //包括最后一天
    var from=parseInt(new Date(this.range.from).getTime()/MINUTE_MS);
    var offset=(parseInt(pg)-1)*this.service.NUM_PER_SMPG;
    var url="/report/brokerage?offset="+offset
        +"&num="+this.service.NUM_PER_SMPG
        +"&from="+from+"&to="+to+"&owner="+this.dtl.owner;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.dtl.list=[];
            this.dtl.max=0;
        } else {
            this.dtl.list=this.formatData(resp.data.list, resp.data.cols);
            this.dtl.max=Math.ceil(resp.data.total/this.service.NUM_PER_SMPG);
        }
    })
},
formatData(rows,cols) {
    var dt=new Date();
    var bts=this.tags.brokerage.types;
    return rows.map(l=>{
        var r={};
        for(var i in cols) {
            r[cols[i]]=l[i];
        }
        dt.setTime(r.createAt*MINUTE_MS);
        r.createAt=datetime2str(dt);
        r.ratio=this.service.formatNum(r.ratio*100,1);
        r.type_s=bts[r.type];
        return r;
    })
},
rangeFilter(dt) {
    var now=new Date().getTime();
    var t=Date.parse(dt);
    return t<=now&&t>=now-YEAR_MS;
},
show_comments(owner) {
    this.cmt.owner=owner;
    this.cmt.dlg=true;
    this.query_cmt(1);
},
query_cmt(pg) {
    var to=parseInt(new Date(this.range.to).getTime()/MINUTE_MS)+1440; //包括最后一天
    var from=parseInt(new Date(this.range.from).getTime()/MINUTE_MS);
    var offset=(parseInt(pg)-1)*this.service.NUM_PER_SMPG;
    var url="/service/workerCmts?supplier="+this.cmt.owner+"&offset="+offset
            +"&num="+this.service.NUM_PER_SMPG+"&from="+from+"&to="+to;
    request({method:"GET", url:url}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.cmt.list=[];
            this.cmt.max=0;
            return;
        }
        this.cmt.max=Math.ceil(resp.data.total/this.service.NUM_PER_SMPG);

        var dt=new Date();
        this.cmt.list=resp.data.list.map(c=>{
            dt.setTime(c.at);
            c.at=datetime2str(dt);
            return c;
        })
    })
},
get_user_tmpl() {
    if(Object.keys(this.user.tmpl).length>0) {
        return new Promise(resolve=>{
            resolve(this.user.tmpl);
        });
    }
    var url="/user/getAppExtTmpl?service=" + this.service.name;
    return request({method:"GET", url:url}, SERVICE_USER).then(resp=>{
        if(resp.code!=RetCode.OK) {
            return {};
        }
        return resp.data.template;
    })
},
show_user(acc) {
    this.get_user_tmpl().then(tmpl=>{
        var url="/userInfo?account="+acc;
        request({method:"GET", url:url}, this.service.name).then(resp=>{
            if(resp.code!=RetCode.OK) {
                this.$refs.errMsg.showErr(resp.code, resp.info);
                return;
            }
            this.user.dlg=true;
            this.user.account=acc;
            var dtl=resp.data;
            var tags=this.tags;
            var segs=[];
            segs.push({n:tags.mobile,v:dtl.mobile});
            segs.push({n:tags.email,v:dtl.email});
            var dt=new Date();
            var year=dt.getFullYear();
            dt.setTime(dtl.createAt);
            segs.push({n:tags.createAt,v:datetime2str(dt)});
            dt.setTime(dtl.birthday*86400000);
            segs.push({n:tags.birth,v:date2str(dt)});
            dtl.age=dt.getFullYear()-year;
            dtl.sex=this.tags.sexInfo[dtl.sex].n;
            if(dtl.ext) {
                dtl.ext=decodeExt(dtl.ext, tmpl);
            } else {
                dtl.ext=decodeExt("{}", tmpl);
            }
            this.user.dtl=dtl;
            this.user.segs=segs;
            this.user.tmpl=tmpl;
        })
    })
},
show_src(type,id) {
    if(type=='ORD') {
        this.$refs.orderDlg.show(id);
    } else {
        this.$refs.serviceDlg.show(id);
    }
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header class="bg-grey-1 text-primary">
   <q-toolbar>
    <q-btn flat round icon="arrow_back" dense @click="service.back"></q-btn>
    <q-toolbar-title>{{tags.brokerage.title}}</q-toolbar-title>
    <q-btn icon="event" flat dense>
     <q-popup-proxy cover transition-show="scale" transition-hide="scale">
      <q-date v-model="range" range :options="rangeFilter">
       <div class="row items-center justify-end">
        <q-btn :label="tags.ok" color="primary" @click="dateChanged" v-close-popup></q-btn>
        <q-btn :label="tags.close" color="primary" flat v-close-popup></q-btn>
       </div>
      </q-date>
     </q-popup-proxy>
     {{range.from}} => {{range.to}}
    </q-btn>
   </q-toolbar>
  </q-header>

  <q-page-container>
    <q-page class="q-pa-md">

<div class="q-pa-lg flex flex-center" v-if="ctrl.max>1">
 <q-pagination v-model="ctrl.cur" color="primary" :max="ctrl.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query"></q-pagination>
</div>
<q-markup-table flat>
 <thead><tr>
  <th class="text-left">{{tags.brokerage.owner}}</th>
  <th class="text-right">{{tags.brokerage.val}}</th>
  <th class="text-right">{{tags.service.cmt}}</th>
 </tr></thead>
 <tbody>
 <tr v-for="v in list" style="cursor:pointer;">
  <td class="text-left" @click="show_user(v.owner)">
   {{v.owner}}
  </td>
  <td class="text-right" @click="show_detail(v.owner)">
   {{v.brokerage}}
  </td>
  <td class="text-right">
    <q-btn icon="comment" @click="show_comments(v.owner)"
     color="primary" flat dense></q-btn>
  </td>
 </tr>
 </tbody>
</q-markup-table>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="dtl.dlg">
 <q-card style="min-width:80vw" class="q-pa-none">
  <q-card-section class="row items-center">
   <div class="text-h6">{{dtl.owner}}</div>
   <q-space></q-space>
   <q-btn icon="close" flat dense v-close-popup></q-btn>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-separator></q-separator>
   <q-markup-table flat>
    <tbody>
      <tr v-for="v in dtl.list">
       <td class="text-left">{{v.createAt}}</td>
       <td class="text-right">{{v.brokerage}}</td>
       <td class="text-right text-primary" @click="show_src(v.type,v.did)" style="cursor:pointer;">
        {{v.type_s}}/{{v.ratio}}%
       </td>
      </tr>
    </tbody>
   </q-markup-table>
   <div class="q-pa-lg flex flex-center" v-if="dtl.max>1">
    <q-pagination v-model="dtl.cur" color="primary" :max="dtl.max" max-pages="10"
     boundary-numbers="false" @update:model-value="query_dtl"></q-pagination>
   </div>
  </q-card-section>
 </q-card>
</q-dialog>

<q-dialog v-model="cmt.dlg">
 <q-card style="min-width:80vw" class="q-pa-none">
  <q-card-section class="row items-center">
   <div class="text-h6">{{cmt.owner}}</div>
   <q-space></q-space>
   <q-btn icon="close" flat dense v-close-popup></q-btn>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-separator></q-separator>
   <div v-if="cmt.list.length>0">
    <q-markup-table flat >
     <tbody>
      <tr v-for="v in cmt.list">
       <td class="text-left">
        <div>{{v.name}}</div>
        <div class="text-caption">{{v.code}}</div>
        <div class="text-caption">{{v.at}}</div>
       </td>
       <td class="text-right">
        <div class="text-caption">{{v.cmt}}</div>
        <q-rating v-model="v.level" size="1em" color="orange" readonly></q-rating>
       </td>
      </tr>
     </tbody>
     </q-markup-table>
    <div class="q-pa-lg flex flex-center" v-if="cmt.max>1">
    <q-pagination v-model="cmt.cur" color="primary" :max="cmt.max" max-pages="10"
     boundary-numbers="false" @update:model-value="query_cmt"></q-pagination>
    </div>
   </div>
   <div v-else>{{tags.service.noCmt}}</div>
  </q-card-section>
 </q-card>
</q-dialog>

<q-dialog v-model="user.dlg">
 <q-card style="min-width:80vw" class="q-pa-none">
  <q-card-section class="row items-center">
   <div class="text-h6">{{user.account}}/{{user.dtl.nickName}}</div>
   <q-space></q-space>
   <q-btn icon="close" flat dense v-close-popup></q-btn>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-separator></q-separator>
   <q-markup-table flat>
    <tr v-for="s in user.segs">
     <th class="text-left">{{s.n}}</th>
     <th class="text-right"><div class="text-body1">{{s.v}}</div></th>
    </tr>
    <tr v-for="e in user.dtl.ext">
     <th class="text-left">{{e.n}}</th>
     <td class="text-right"><div class="text-body1">{{e.v}}</div></td>
    </tr>
   </q-markup-table>
  </q-card-section>
 </q-card>
</q-dialog>

<service-dlg :tags="tags" :alertDlg="alertDlg" :confirmDlg="confirmDlg" :role="role" ref="serviceDlg"></service-dlg>
<order-dlg :tags="tags" :alertDlg="alertDlg" :confirmDlg="confirmDlg" :role="role" ref="orderDlg"></order-dlg>
<component-confirm-dialog :title="tags.alert" :close="tags.cancel" :ok="tags.ok" ref="confirmDlg"></component-confirm-dialog>
<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></component-alert-dialog>
`
}