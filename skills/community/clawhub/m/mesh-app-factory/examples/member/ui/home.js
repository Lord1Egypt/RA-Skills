export default {
inject:['service', 'tags'],
data() {return {
    isOwner:false,
    vips:[], //会员列表
    search:'',
    vipPg:{cur:1,max:0,searchTag:''},
    newVip:{name:'',mobile:'',pwd:'',sex:'',birth:'',dlg:false}
}},
created(){
    var url="/power/get?service="+this.service.name;
    request({method:"GET",url:url}, SERVICE_USER).then(resp=>{
        if(resp.code!=0) {
            Console.warn("request "+url+" failed:" + resp.code + ",info:" + resp.info);
            return;
        }
        this.isOwner=resp.data.role=='admin';
    }); 
    this.query_vips(0);
},
methods:{
query_vips(offset) {
    this.search="";
    var url="/api/vip/list?offset="+offset+"&num="+this.service.NUM_PER_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.vips=[];
            this.vipPg.max=0;
            this.vipPg.searchTag=this.tags.search;
        } else {
            this.formatData(resp.data.vips);
            this.vipPg.max=Math.ceil(resp.data.total/this.service.NUM_PER_PAGE);
            this.vipPg.searchTag=this.tags.search + '(' + resp.data.total + ')';
        }
    })
},
search_vips() {
    if(this.search=='') {
        this.query_vips(0);
        return;
    }
    var url="/api/vip/search?s="+this.search+"&limit="+this.service.NUM_PER_PAGE
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.formatData(resp.data.vips);
        this.vipPg.max=1;
    })
},
formatData(rows) {
    var vips=[];
    var dt=new Date();
    var updAt, birth, age;
    var nowYear = dt.getFullYear();
    for(var r of rows) {
        dt.setTime(r.update_time);
        updAt = dt.toLocaleDateString();
        dt.setTime(r.birth*86400000);
        age=nowYear-dt.getFullYear();
        birth = dt.toLocaleDateString();
        vips.push({id:r.id, name:r.name, birth:birth, updateAt:updAt,
            sex:this.tags.sexInfo[r.sex].n, age:age});
    }
    this.vips=vips;
},
add_vip() {
    var url="/api/vip/add";
    var d=this.newVip;
    var birth=Math.round(new Date(d.birth).getTime()/86400000);
    var reqDta={name:d.name, mobile:d.mobile, pwd:d.pwd, sex:d.sex, birth:birth};
    request({method:"POST",url:url,data:reqDta}, this.service.name).then(resp => {
        if(resp.code != 0) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.newVip.dlg=false;
        this.query_vips(0);
    })
},
change_vip_page(page) {
    this.query_vips((parseInt(page)-1)*this.service.NUM_PER_PAGE);
},
open_newvip_dlg() {
    this.newVip={name:'',mobile:'',pwd:'',birth:'',sex:'', dlg:true};
}
},

template:`
<q-layout view="hHh lpr fFf">
  <q-header class="bg-grey-1 text-primary" elevated>
   <q-toolbar>
    <q-avatar square><img src="./favicon.png"></q-avatar>
    <q-toolbar-title>{{tags.app_name}}</q-toolbar-title>
    <q-btn flat round dense icon="menu" v-if="isOwner">
     <q-menu>
      <q-list style="min-width: 100px">
        <q-item clickable v-close-popup @click="service.jumpTo('/reports')">
          <q-item-section>{{tags.reports}}</q-item-section>
        </q-item>
        <q-item clickable v-close-popup @click="service.jumpTo('/settings')">
          <q-item-section>{{tags.settings}}</q-item-section>
        </q-item>
        <q-separator></q-separator>
       </q-list>
     </q-menu>
    </q-btn>
   </q-toolbar>
  </q-header>
  <q-footer class="bg-white q-pa-md">
    <q-input outlined v-model="search" :label="vipPg.searchTag" dense @keyup.enter="search_vips">
    <template v-slot:append>
      <q-icon name="close" v-show="search!==''" @click="query_vips(0)" class="cursor-pointer q-mr-md"></q-icon>
      <q-icon name="search" @click="search_vips" class="cursor-pointer q-mr-md"></q-icon>
    </template>
    <template v-slot:after>
      <q-btn round color="primary" icon="add_circle" @click="open_newvip_dlg"></q-btn>
    </template>
    </q-input>
  </q-footer>

  <q-page-container>
    <q-page class="q-pa-md">
<div class="q-pa-lg flex flex-center" v-if="vipPg.max>1">
 <q-pagination v-model="vipPg.cur" color="primary" :max="vipPg.max" max-pages="10"
  boundary-numbers="false" @update:model-value="change_vip_page"></q-pagination>
</div>
<q-markup-table flat>
 <thead><tr>
  <th class="text-left">{{tags.vip}}</th>
  <th class="text-right">{{tags.updateAt}}</th>
 </tr></thead>
 <tbody>
 <tr v-for="v in vips" @click="service.jumpTo('/vip?id='+v.id)">
  <td class="text-left"><list dense><q-item-section>
    <q-item-label>{{v.name}}({{v.sex}}, {{v.age}})</q-item-label>
    <q-item-label caption>{{tags.birth}}:{{v.birth}}</q-item-label>
   </q-item-section></list></td>
  <td class="text-right">{{v.updateAt}}</td>
 </tr>
 </tbody>
</q-markup-table>
    </q-page>
  </q-page-container>
</q-layout>
    
<q-dialog v-model="newVip.dlg">
  <q-card style="min-width:70vw" class="q-pa-md">
    <q-card-section>
      <div class="text-h6">{{tags.addVip}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
     <q-input v-model="newVip.name" :label="tags.name" dense
     :rules="[v=>v!=''|| tags.namePls]"></q-input>
     <q-input v-model="newVip.mobile" :label="tags.mobile" maxlength=11
     :rules="[v=>/^1[0-9]{10}$/.test(v)|| tags.mobilePls]" dense></q-input>
     <q-input v-model="newVip.pwd" :label="tags.pwd" type="password" dense
     :rules="[/^[0-9]{4,20}$/.test(v)|| tags.pwdPls]"></q-input>
      <component-date-input :close="tags.ok" :label="tags.birth" v-model="newVip.birth" max="today"></component-date-input>
     <div class="q-gutter-sm">
      <q-radio v-model="newVip.sex" val="F" :label="tags.sexInfo.F.n"></q-radio>
      <q-radio v-model="newVip.sex" val="M" :label="tags.sexInfo.M.n"></q-radio>
     </div>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
      <q-btn :label="tags.ok" color="primary" @click="add_vip"></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></component-alert-dialog>
`
}